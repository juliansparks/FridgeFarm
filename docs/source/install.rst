============
Installation
============

#. Clone the repo

   .. code-block:: bash
  
      git clone 'https://github.com/juliansparks/CEN-4010'
  
#. Change directory to the repo

   .. code-block:: bash

      cd CEN-4010
  
#. Check out the ``flask_app`` branch

   .. code-block:: bash

      git checkout flask_app
  
#. Create a virtual environment

   .. code-block:: bash
     
      python3.6 -m venv venv

#. Activate the virtual environment

   .. code-block:: bash

      source venv/bin/activate

#. Upgrade pip

   .. code-block:: bash

      pip install --upgrade pip
      
#. Install dependencies

   .. code-block:: bash

      pip install -r requirements.txt

#. Set environment variables
   
   .. code-block:: bash

      export FLASK_DEBUG=1
      export FLASK_APP=fapi.py

#. Run the development server

   .. code-block:: bash

      flask run

   or to bind to all interfaces

   .. code-block:: bash

      flask run --host='0.0.0.0'
      
