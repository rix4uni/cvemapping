from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import shutil
import importlib
import importlib.machinery

app = FastAPI()
router = APIRouter()

class ExtensionMountingInfos(BaseModel):
    category: str
    folder: str
    client_id: str
    language: str

class ExtensionInstallInfos(BaseModel):
    name: str = None

class LollmsPaths:
    extensions_zoo_path: Path = Path("/path/to/extensions_zoo_path")

class InstallOption:
    INSTALL_IF_NECESSARY = "install_if_necessary"

class LOLLMSExtension:
    def __init__(self, app, installation_option):
        self.app = app
        self.installation_option = installation_option

class ExtensionBuilder:
    def build_extension(
        self, 
        extension_path: str, 
        lollms_paths: LollmsPaths,
        app: FastAPI,
        installation_option: InstallOption = InstallOption.INSTALL_IF_NECESSARY
    ) -> LOLLMSExtension:
        extension, script_path = self.getExtension(extension_path, lollms_paths, app)
        return extension(app=app, installation_option=installation_option)
    
    def getExtension(
        self, 
        extension_path: str, 
        lollms_paths: LollmsPaths,
        app: FastAPI
    ) -> (LOLLMSExtension, Path):
        extension_path = lollms_paths.extensions_zoo_path / extension_path
        absolute_path = extension_path.resolve()
        module_name = extension_path.stem
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        extension_module = loader.load_module()
        extension: LOLLMSExtension = getattr(extension_module, extension_module.extension_name)
        return extension, absolute_path

def sanitize_path(path: str) -> str:
    return path.strip("/")

def check_access(server, client_id):
    # Dummy access check
    pass

@app.post("/mount_extension")
def mount_extension(data: ExtensionMountingInfos):
    check_access(None, data.client_id)
    print("- Mounting extension")
    category = sanitize_path(data.category)
    name = sanitize_path(data.folder)

    package_path = f"{category}/{name}"
    package_full_path = Path("/path/to/extensions_zoo_path") / package_path
    config_file = package_full_path / "config.yaml"
    if config_file.exists():
        # Dummy server config
        server_config = {"extensions": []}
        server_config["extensions"].append(package_path)
        # Dummy rebuild_extensions
        print("Rebuilding extensions...")

    return {"status": "success"}

@app.post("/install_extension")
def install_extension(data: ExtensionInstallInfos):
    lollmsElfServer = None
    if not data.name:
        try:
            data.name = lollmsElfServer.config.extensions[-1]
        except Exception as ex:
            print(ex)
            return {"status": False}
    
    try:
        extension_path = Path("/path/to/extensions_zoo_path") / data.name
        print(f"- Reinstalling extension {data.name}...")
        
        if not extension_path.is_file():
            return {"status": False, "error": "Extension file not found or is corrupted"}
        
        try:
            mounted_extensions = []
            mounted_extensions.append(
                ExtensionBuilder().build_extension(extension_path, lollmsElfServer)
            )
            return {"status": True}
        except Exception as ex:
            print(f"Extension file error: {ex}")
            return {"status": False, 'error': str(ex)}

    except Exception as e:
        return {"status": False, 'error': str(e)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        upload_directory = Path("/path/to/uploads")
        upload_directory.mkdir(parents=True, exist_ok=True)
        file_path = upload_directory / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"File uploaded successfully: {file_path}")
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    try:
        file_path = Path("/path/to/uploads") / filename
        if file_path.exists():
            return FileResponse(file_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example extension module registration
from fastapi import APIRouter

extension_router = APIRouter()

def setup_extension(app: FastAPI):
    app.include_router(extension_router)

# Setup extensions
setup_extension(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9600)