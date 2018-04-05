===============================
Generating Sphinx Documentation
===============================

#. Change directory to the repo

   .. code-block:: bash

      cd CEN-4010
  
#. Check out the ``flask_app`` branch

   .. code-block:: bash

      git checkout flask_app

#. Change directory to the ``docs`` directory

   .. code-block:: bash

      cd docs/

#. Make HTML documentation

   .. code-block:: bash

      make html

The resulting HTML will be in ``docs/build/html``.
You can use python's ``http.server`` to host this directory locally
by typing the following.

.. code-block:: bash

   cd CEN-4010/docs/build/html
   python -m http.server 5000
  
