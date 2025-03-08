from fastapi import FastAPI
from controllers.exercises_controller import router as exercises_router
from controllers.book_controller import router as books_router

app = FastAPI()

app.include_router(exercises_router)
app.include_router(books_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
