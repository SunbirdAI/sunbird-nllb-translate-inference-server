import runpod
import os
from dotenv import load_dotenv
import time
from pprint import PrettyPrinter
import asyncio
import aiohttp
from runpod import AsyncioEndpoint, AsyncioJob
import json

pprint = PrettyPrinter(indent=2)

load_dotenv()

runpod.api_key = os.getenv("RUNPOD_API_KEY")

endpoint = runpod.Endpoint(os.getenv("ENDPOINT_ID"))


endpoint_health = endpoint.health()
print(json.dumps(endpoint_health, indent=2))


def synchronous_run():
    start_time = time.time()
    try:
        run_request = endpoint.run_sync(
            {
                "input": {
                    "source_language": "lug",
                    "target_language": "eng",
                    "text": "Ekibiina ekiddukanya omuzannyo gw’emisinde mu ggwanga ekya Uganda Athletics Federation kivuddeyo nekitegeeza nga lawundi esooka eyemisinde egisunsulamu abaddusi abanakiika mu mpaka ezenjawulo ebweru w’eggwanga egya National Athletics Trials nga bwegisaziddwamu.",
                }
            },
            timeout=60,  # Timeout in seconds.
        )

        pprint.pprint(run_request)
    except TimeoutError:
        print("Job timed out.")

    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")


def asynchronous_run():
    start_time = time.time()
    input_payload = {
        "input": {
            "source_language": "lug",
            "target_language": "eng",
            "text": "Ekibiina ekiddukanya omuzannyo gw’emisinde mu ggwanga ekya Uganda Athletics Federation kivuddeyo nekitegeeza nga lawundi esooka eyemisinde egisunsulamu abaddusi abanakiika mu mpaka ezenjawulo ebweru w’eggwanga egya National Athletics Trials nga bwegisaziddwamu.",
        }
    }

    try:
        run_request = endpoint.run(input_payload)

        # Initial check without blocking, useful for quick tasks
        status = run_request.status()
        print(f"Initial job status: {status}")

        if status != "COMPLETED":
            # Polling with timeout for long-running tasks
            output = run_request.output(timeout=60)
        else:
            output = run_request.output()
        pprint.pprint(f"Job output: {output}")
    except Exception as e:
        print(f"An error occurred: {e}")

    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")


# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # For Windows users.


async def asyncio_run():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        input_payload = {
            "source_language": "lug",
            "target_language": "eng",
            "text": "Ekibiina ekiddukanya omuzannyo gw’emisinde mu ggwanga ekya Uganda Athletics Federation kivuddeyo nekitegeeza nga lawundi esooka eyemisinde egisunsulamu abaddusi abanakiika mu mpaka ezenjawulo ebweru w’eggwanga egya National Athletics Trials nga bwegisaziddwamu.",
        }
        endpoint = AsyncioEndpoint(os.getenv("ENDPOINT_ID"), session)
        job: AsyncioJob = await endpoint.run(input_payload)

        # Polling job status
        while True:
            status = await job.status()
            print(f"Current job status: {status}")
            if status == "COMPLETED":
                output = await job.output()
                pprint.pprint(f"Job output: {output}")
                break  # Exit the loop once the job is completed.
            elif status in ["FAILED"]:
                print("Job failed or encountered an error.")

                break
            else:
                print("Job in queue or processing. Waiting 3 seconds...")
                await asyncio.sleep(3)  # Wait for 3 seconds before polling again

    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")


if __name__ == "__main__":
    synchronous_run()
    asynchronous_run()
    asyncio.run(asyncio_run())
