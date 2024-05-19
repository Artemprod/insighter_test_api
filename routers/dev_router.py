from fastapi import HTTPException, APIRouter, Request, Path
from app.publishers.publisher import Publisher

# Создание экземпляра роутера
dev_router = APIRouter(
    prefix="/development",
    tags=["Endpoints for development"],
)
publisher = Publisher("nats://demo.nats.io:4222")

@dev_router.get("/assistant/get_all")
async def get_all_assistants(request: Request):
    try:
        # Фиктивные данные
        assistants = [
            {"id": 1, "name": "Assistant One", "role": "Helper"},
            {"id": 2, "name": "Assistant Two", "role": "Guide"}
        ]
        return assistants
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Фиктивные базы данных
assistant_db = {
    1: {"id": 1, "name": "Assistant One", "role": "Helper"},
    2: {"id": 2, "name": "Assistant Two", "role": "Supporter"}
}
transcribed_text_db = {
    1: {"id": 1, "text": "This is a transcribed text."},
    2: {"id": 2, "text": "Another transcribed text."}
}
summary_text_db = {
    1: {"id": 1, "summary": "This is a summary of the text."},
    2: {"id": 2, "summary": "This is another summary."}
}

@dev_router.get("/assistant/get_one/{id}")
async def get_one_assistant(id: int = Path(..., description="The ID of the assistant to retrieve")):
    try:
        if id in assistant_db:
            return assistant_db[id]
        else:
            raise HTTPException(status_code=404, detail="Assistant not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@dev_router.get("/result/get_transcribed_text/{id}")
async def get_transcribed_text(id: int = Path(..., description="The ID of the transcribed text to retrieve")):
    try:
        if id in transcribed_text_db:
            result = transcribed_text_db[id]
            await publisher.publish_result({"status": "summary_ready", "id": result["id"]}, "summary_queue")
            return result
        else:
            raise HTTPException(status_code=404, detail="Transcribed text not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@dev_router.get("/result/get_summary_text/{id}")
async def get_summary_text(id: int = Path(..., description="The ID of the summary text to retrieve")):
    try:
        if id in summary_text_db:
            return summary_text_db[id]
        else:
            raise HTTPException(status_code=404, detail="Summary text not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@dev_router.post("/start/youtube")
async def start_youtube(request: Request):
    try:
        # Фиктивные данные
        response = {"status": "YouTube processing started", "id": 1}
        await publisher.publish_result({"status": "transcribed_text_ready", "id": 1}, "youtube_queue")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@dev_router.post("/start/storage")
async def start_storage(request: Request):
    try:
        # Фиктивные данные
        response = {"status": "Storage processing started", "id": 2}
        await publisher.publish_result({"status": "transcribed_text_ready", "id": 2}, "storage_queue")
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")