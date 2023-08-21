from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()


async def translate_text(source_text, target_lang):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "auto",
                "tl": target_lang,
                "dt": "t",
                "q": source_text,
            },
        )
        translation = response.json()[0][0][0]
        return translation


@app.post("/translate/")
async def translate(source_lang: str, target_lang: str, text: str):
    try:
        translation = await translate_text(text, target_lang)
        return {"translation": translation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
