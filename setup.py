from distutils.core import setup
setup(
  name = 'cartpy',         # How you named your package folder (MyLib)
  packages = ['cartpy'],   # Chose the same as "name"
  version = '0.2.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Cartpy offers an easy way to access the IBGE cartographic databases',   # Give a short description about your library
  author = 'Lucas Cavalcanti Rodrigues',                   # Type in your name
  author_email = 'lucas.ecomg@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/lucascr91/cartpy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/lucascr91/cartpy/archive/v_0.2.0.tar.gz', 
  package_dir={'cartpy': 'cartpy'},
  package_data={'cartpy': ['data/*.csv']},
  include_package_data=True,
  keywords = ['Brazil', 'municipality', 'geodata'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
          'fuzzywuzzy'
                ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)