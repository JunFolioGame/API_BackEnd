from core.containers import ProjectContainer
from players.dto import CreatePlayerDTO
from players.exceptions import PlayerDoesNotExist


def uuid_required(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        player_uuid = request.COOKIES.get("PLAYER_UUID", None)
        player_username = request.COOKIES.get("PLAYER_USERNAME", None)
        interactor = ProjectContainer.player_interactor()
        api_adress = request.META.get("REMOTE_ADDR")
        browser_info = request.META.get("HTTP_USER_AGENT")
        if not player_uuid:
            try:
                player = interactor.get_player_by_options(
                    CreatePlayerDTO(api_adress=api_adress, browser_info=browser_info)
                )
            except PlayerDoesNotExist:
                player = interactor.create_player(
                    player=CreatePlayerDTO(api_adress=api_adress, browser_info=browser_info)
                )
            finally:
                player_uuid = player.player_uuid
                player_username = player.username
        request.COOKIES["PLAYER_UUID"] = player_uuid
        request.COOKIES["PLAYER_USERNAME"] = player_username
        response = func(*args, **kwargs)
        response.set_cookie("PLAYER_USERNAME", player_username)
        response.set_cookie("PLAYER_UUID", player_uuid)
        return response

    return wrapper
