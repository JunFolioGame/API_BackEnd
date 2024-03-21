from core.containers import ProjectContainer


def uuid_required(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        player_uuid = request.COOKIES.get("PLAYER_UUID", None)
        interactor = ProjectContainer.player_interactor()
        if not player_uuid:
            player = interactor.create_player()
            player_uuid = player.player_uuid
        request.COOKIES["PLAYER_UUID"] = player_uuid
        response = func(*args, **kwargs)
        response.set_cookie("PLAYER_UUID", player_uuid)
        return response

    return wrapper
