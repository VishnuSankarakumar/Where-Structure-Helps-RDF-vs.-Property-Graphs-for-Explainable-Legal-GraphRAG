import json, glob, os, sys

from openai import AsyncOpenAI
from ragas import SingleTurnSample, EvaluationDataset, evaluate
from ragas.llms import llm_factory
from ragas.run_config import RunConfig



from ragas.metrics._faithfulness import Faithfulness
from ragas.metrics._context_precision import LLMContextPrecisionWithReference
from ragas.metrics._context_recall import LLMContextRecall

os.environ["OPENAI_API_KEY"] = "REDACTED"

if len(sys.argv) != 4:
    print("how to use: python evaluate_neo4j.py [answers_folder] [ground_truth_folder] [output_file]")
    sys.exit(1)

neo4j_dir, gt_dir, output_csv = sys.argv[1], sys.argv[2], sys.argv[3]

client = AsyncOpenAI()
llm = llm_factory("gpt-4o-mini", client=client, max_tokens=16000)

#build samples
samples = []
for neo4j_file in sorted(glob.glob(os.path.join(neo4j_dir, "*.json"))):
    name = os.path.splitext(os.path.basename(neo4j_file))[0] #strip json to match ground truth file name
    gt_file = os.path.join(gt_dir, name + ".txt")

    if not os.path.exists(gt_file):
        print(f"SKIP {name}") #no ground truth found so skip silently
        continue

    with open(neo4j_file, encoding="utf-8") as f:
        data = json.load(f)

    mode = list(data["chatResponse"]["modes"].values())[0] #assume chat response only has one value
    chunks = [c["text"] for c in data.get("chunks", [])] #retrieved context chunks

    with open(gt_file, encoding="utf-8") as f:
        reference = f.read().strip()

    if chunks:
        retrieved_contexts = chunks #get context from chunks if its there
    else:
        retrieved_contexts = [mode.get("metric_contexts", "")] #otherwise extract from metric_contexts

    samples.append(SingleTurnSample(
        user_input=mode["metric_question"],
        response=mode["metric_answer"],
        retrieved_contexts=retrieved_contexts,
        reference=reference,
    ))
    print(f"OK {name}")

if not samples:
    print("ERROR no samples")
    sys.exit(1)

print(f"{len(samples)} samples loaded running eval\n")

result = evaluate(
    dataset=EvaluationDataset(samples=samples),
    metrics=[Faithfulness(), LLMContextPrecisionWithReference(), LLMContextRecall()],
    llm=llm,
    run_config=RunConfig(timeout=120, max_retries=3, max_workers=8), #high timeout because llms slow
    raise_exceptions=False, #any failures should not crash the whole run
)

df = result.to_pandas()
df.to_csv(output_csv, index=False)
print(f"Saved to {output_csv}")
print(df.to_string())