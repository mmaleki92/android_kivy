from pythonforandroid.recipe import PythonRecipe
from os.path import join

class OpenCVRecipe(PythonRecipe):
    version = '4.8.0.76'
    url = 'https://github.com/opencv/opencv-python/archive/{version}.zip'
    depends = ['numpy', 'setuptools']
    site_packages_name = 'cv2'
    call_hostpython_via_targetpython = False
    
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['PYTHONPATH'] = ':'.join([
            self.ctx.get_site_packages_dir(),
            env['PYTHONPATH'] if 'PYTHONPATH' in env else ''
        ])
        return env

recipe = OpenCVRecipe()