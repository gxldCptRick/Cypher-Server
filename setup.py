from distutils.core import setup

setup(name='cypher_server',
      version='0.1',
      description='A simple server that will use the cypher_app to encrypt and decrypt the messages given to it.',
      url='https://github.com/gxldCptRick/Cypher-Server.git',
      author='GXLD CPT RICK',
      author_email='andreshcar@live.com',
      license='Apache License 2.0',
      packages=['cypher_server'],
      install_requires=[
          'cypher_app', 'flask', 'flask_cors'
      ],
      zip_safe=False)
