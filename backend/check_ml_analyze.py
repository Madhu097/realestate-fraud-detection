try:
    import app.routers.ml_analyze
    print("ml_analyze imported successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
