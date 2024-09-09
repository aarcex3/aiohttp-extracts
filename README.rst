Parameter Extraction Classes
Aiohttp Extracts
=============================

This document provides a description and example usage of various parameter extraction classes.

Classes
-------

Header
^^^^^^
Extracts a value from the request headers.

.. literalinclude:: ../examples/header.py
   :language: python
   :caption: Example usage of Header extraction


Query
^^^^^^
Extracts a value from the request queries.

.. literalinclude:: ../examples/query.py
   :language: python
   :caption: Example usage of Query extraction


Cookie
^^^^^^
Extracts a value from the request cookies.

.. literalinclude:: ../examples/cookie.py
   :language: python
   :caption: Example usage of Cookie extraction

File
^^^^^^
Extracts a value from the request posts.

.. literalinclude:: ../examples/file.py
   :language: python
   :caption: Example usage of File extraction


Path
^^^^^^
Extracts a value from the request match info.

.. literalinclude:: ../examples/path.py
   :language: python
   :caption: Example usage of Path extraction


ReqBody
^^^^^^
Extracts a value from the request json.

.. literalinclude:: ../examples/reqbody.py
   :language: python
   :caption: Example usage of ReqBody extraction


RequestAttr
^^^^^^
Extracts a value from the request attributes.

.. literalinclude:: ../examples/request_attr.py
   :language: python
   :caption: Example usage of RequestAttr extraction