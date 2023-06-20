from app.contollers.load_data_controllers import LoadFixturesController


async def load_data() -> None:
    await LoadFixturesController.load_data()
    return
