from scripts.lobby.lobby import Lobby
from scripts.lobby.lobbyParameters import HEIGHT_SCREEN, WIDTH_SCREEN


if __name__ == '__main__':
    lobby_scene = Lobby(parent=None, selected_positioning=None, height=HEIGHT_SCREEN, width=WIDTH_SCREEN)
    lobby_scene.start_lobby()
