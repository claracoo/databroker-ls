from ._version import get_versions
import intake

__version__ = get_versions()["version"]
del get_versions

catalog_class = intake.registry["bluesky-mongo-normalized-catalog"]

databroker_ls_catalog_instance = catalog_class(
   metadatastore_db="mongodb://localhost:27017/md",
   asset_registry_db="mongodb://localhost:27017/ar"
)
