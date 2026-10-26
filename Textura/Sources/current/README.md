# Sources

`sources.py` registers a supplied original or URL metadata, and requests a local extraction from Reading. `current/records/<source-id>/manifest.json` identifies an immutable `original.*` file and its digest. The provided filename remains metadata. Capture scope is explicit and defaults to unknown; publication date and author remain unknown until established.

No web crawler is implemented. Use the current AI host's authorized public browsing capability to obtain material, then register the actual obtained file. Record any missing pages, dynamic content, assets, provenance chain or source context in the research record. A saved HTML file is not necessarily a complete interactive website. A URL registration does not claim full-text capture. Ordinary search candidates can remain bibliographic leads; preserve actually used evidence when available.

Local originals can have any language or supported filename. Internal directories use stable ASCII IDs. Later captures get new IDs and explicit version/derivation relationships; never replace an acquired original. Maximum initial capture size is 256 MiB; larger files require a deliberate adapter update. Extraction does not grant a verified status to a source.
