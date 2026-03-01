import pygame
from numpy import ndarray, array_equal
from json import load, dump
from hashlib import sha256
from pathlib import Path

def surface_hash(surface: pygame.Surface) -> str:
    raw = pygame.image.tobytes(surface, "RGBA")
    return sha256(raw).hexdigest()

type ConnectionType = tuple[int, int, int, int]
type ConnectionsType = tuple[ConnectionType, ...]

class Tilesets:
    TILESET_PATH: Path = Path("./assets/WFC/tileset/")
    CACHE_PATH: Path = Path("./src/visualizations/visualizers/wave_function_collapse/tile_cache/")
    TILESETS: list[str] = []
    TILES_COUNT: dict[str, int] = {}
    TILES_IMGS: dict[str, tuple[pygame.Surface, ...]] = {}
    TILES_CONNECTIONS: dict[str, ConnectionsType] = {}
    VERSION: int = 0
    COLORKEY: tuple[int, int, int] = (0, 0, 0)

    initialized: bool = False

    @classmethod
    def init(cls: Tilesets) -> None:
        if not cls.TILESET_PATH.exists():
            raise FileNotFoundError(f"'tileset' directory doesn't exist at {cls.TILESET_PATH}")
        
        cls.load_all_tilesets()

        cls.initialized = True

    
    @classmethod
    def load_all_tilesets(cls: Tilesets) -> None:
        tilesets: list[Path] = [path for path in cls.TILESET_PATH.iterdir()]
        if not tilesets:
            raise FileNotFoundError(f"No tilesets found at {cls.TILESET_PATH}")
        
        for tileset_path in tilesets:
            tileset_name, tileset_dims, tiles_count = tileset_path.name.split('.')[0].split('_')
            rows, cols = map(int, tileset_dims.split('x'))
            tiles_count: int = int(tiles_count)
            cls.load_tileset(tileset_path, tileset_name, rows, cols, tiles_count)

    @classmethod
    def load_tileset(cls: Tilesets, tileset_path: Path, tileset_name: str, rows: int, cols: int, tiles_count: int) -> None:
        tileset_img: pygame.Surface = pygame.image.load(tileset_path)
        tileset_rect: pygame.Rect = tileset_img.get_rect()
        
        cls.TILESETS.append(tileset_name)
        cls.TILES_IMGS[tileset_name] = cls.get_tiles_from_tileset(tileset_img, rows, cols, tileset_rect.width//cols, tiles_count, tileset_name)
        cls.TILES_COUNT[tileset_name] = len(cls.TILES_IMGS[tileset_name])
        cls.TILES_CONNECTIONS[tileset_name] = cls.get_tileset_connections(tileset_name)
    
    @classmethod
    def get_tiles_from_tileset(cls: Tilesets, tileset_img: pygame.Surface, rows: int, cols: int, size: int, tiles_count: int, tileset_name) -> tuple[pygame.Surface]:
        tiles: list[pygame.Surface] = []
        tile_index: int = 0
        for row in range(rows):
            for col in range(cols):
                image: pygame.Surface = pygame.Surface((size, size))
                image.blit(tileset_img, (-col*size, -row*size))
                
                images: list[pygame.Surface] = cls.get_tile_variations(image)
                tiles.extend(images)
                
                tile_index += 1
                if tile_index >= tiles_count:
                    break
            else:
                continue
            break

        return tuple(tiles)

                
    @classmethod
    def get_tile_variations(cls: Tilesets, image: pygame.Surface) -> list[pygame.Surface]:
        images: list[pygame.Surface] = [image]
        
        # Rotations
        for _ in range(3):
            images.append(pygame.transform.rotate(images[-1], -90))

        # Flips
        images.append(pygame.transform.flip(image, True, False)) # Vertical Flip
        images.append(pygame.transform.flip(image, False, True)) # Horizontal Flip

        # Removing duplicate images
        unique_images: list[pygame.Surface] = []
        seen_hashes: set[str] = set()
        for image in images:
            image = image.convert_alpha()
            image_hash: str = surface_hash(image)
            if image_hash in seen_hashes:
                continue
            unique_images.append(image)
            seen_hashes.add(image_hash)
        
        return unique_images

    @classmethod
    def get_tile_edges(cls: Tilesets, tile: pygame.Surface) -> tuple[ndarray, ndarray, ndarray, ndarray]:
        tile_array: ndarray = pygame.surfarray.array3d(tile)
        
        # (UP, RIGHT, DOWN, LEFT)
        return (tile_array[:, 0, :], tile_array[-1, :, :], tile_array[:, -1, :], tile_array[0, :, :])

    @classmethod
    def get_tileset_connections(cls: Tilesets, tileset_name: str) -> ConnectionsType:
        connection_cache_path: Path = cls.CACHE_PATH / f"{tileset_name}_generated.json"
        if connection_cache_path.exists():
            with open(connection_cache_path, 'r') as file:
                generated: dict[str, int | ConnectionsType] = load(file)
                if generated["version"] == cls.VERSION:
                    return tuple(tuple(row) for row in generated["connections"])
        
        edges: tuple[tuple[ndarray]] = tuple(cls.get_tile_edges(tile) for tile in cls.TILES_IMGS[tileset_name])
        return cls.get_connections_from_edges(tileset_name, edges)
    
    @classmethod
    def get_connections_from_edges(cls: Tilesets, tileset_name:str, edges: tuple[tuple[ndarray]]) -> ConnectionsType:
        tiles_count: int = cls.TILES_COUNT[tileset_name]
        connections: list[list[int]] = [[(1 << tiles_count) - 1 for _ in range(4)] for _ in range(tiles_count)]

        for index1, tile1_edges in enumerate(edges):
            for index2, tile2_edges in enumerate(edges):
                for direction in range(4):
                    if not array_equal(tile1_edges[direction], tile2_edges[(direction + 2) % 4]):
                        connections[index1][direction] &= ~(1 << index2)
            connections[index1] = tuple(connections[index1])
        
        cls.cache_connections(tileset_name, connections)
        return connections

    @classmethod
    def cache_connections(cls: Tilesets, tileset_name: str, connections: ConnectionsType) -> None:
        data: dict[str, int | ConnectionsType] = {"version": cls.VERSION, "connections": connections}
        connection_cache_path: Path = cls.CACHE_PATH / f"{tileset_name}_generated.json"
        with open(connection_cache_path, 'w') as file:
            dump(data, file)
    
    @classmethod
    def get_tile_image(cls: Tilesets, tileset_type: str, tile_index: int) -> pygame.Surface:
        return cls.TILES_IMGS[tileset_type][tile_index]
    
    @classmethod
    def get_tile_connection(cls: Tilesets, tileset_type: str, tile_index: int, direction: int) -> ConnectionType:
        return cls.TILES_CONNECTIONS[tileset_type][tile_index][direction]
    
#     @classmethod
#     def debug_save_surface(cls: Tilesets, images, filename: str):
#         surface: pygame.Surface = pygame.Surface((280, 224))
#         surface.fill((255, 255, 255))
    
#     @classmethod
#     def debug_save(cls: Tilesets, image, filename: str):
#         path: Path = Path("D:/Programming/Python/algorithm-visualizations/assets/WFC/test")
#         pygame.image.save(image, path / filename)
    
#     @classmethod
#     def debug(cls: Tilesets) -> None:
#         # cls.debug_save(Tilesets.TILES_IMGS["castle"][0], "castle/0.png")
#         cls.debug_save(pygame.image.load(Tilesets.TILESET_PATH / "castle_3x4_11.png"), "castle/all.png")
#         rows: int = 6
#         cols: int = 7
#         padding = 10
#         # # print(len(cls.TILES_IMGS["castle"]))
#         # surface: pygame.Surface = pygame.Surface((cols*(60 + padding), rows*(60 + padding)))
#         # for idx, image in enumerate(cls.TILES_IMGS["circuit"]):
#         #     surface.blit(image, ((idx%cols)*56 + padding*(idx%cols), (idx//cols)*56 + padding*(idx//cols)))
#         # cls.debug_save(surface, f"all_circuit.png")

#         surface: pygame.Surface = pygame.Surface((cols*(60 + padding), rows*(60 + padding)))
#         for idx, image in enumerate(cls.TILES_IMGS["castle"]):
#             surface.blit(image, ((idx%cols)*56 + padding*(idx%cols), (idx//cols)*56 + padding*(idx//cols)))
#         cls.debug_save(surface, f"all_castle.png")

#         # tileset_type: str = "castle"

#         # cols: int = 40
#         # col: int = 0
#         # padding: int = 5
#         # surface: pygame.Surface = pygame.Surface((cols*(56 + padding), cols*(56 + padding)))
#         # for index1, tile1 in enumerate(cls.TILES_IMGS[tileset_type]):
#         #     for index2, tile2 in enumerate(cls.TILES_IMGS[tileset_type]):
#         #         if cls.TILES_CONNECTIONS[tileset_type][index1][2] & (1 << index2) and cls.TILES_CONNECTIONS[tileset_type][index2][0] & (1 << index1):
#         #             surface.blit(tile1, ((col%cols)*(56 + padding), (col//cols)*2*(56 + padding)))
#         #             surface.blit(tile2, ((col%cols)*(56 + padding), (col//cols)*2*(56 + padding) + 56))
#         #             col += 1
#         # cls.debug_save(surface, f"{tileset_type}_connections.png")

# def main() -> None:
#     pygame.init()
#     pygame.display.set_mode((500, 500))
#     Tilesets.init()
#     Tilesets.debug()
#     pygame.quit()

# if __name__ == "__main__":
#     main()