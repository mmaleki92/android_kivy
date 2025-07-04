from pythonforandroid.recipe import PythonRecipe
from os.path import join
import os
import sh

class OpenCVRecipe(PythonRecipe):
    version = '4.8.0.76'
    url = 'https://github.com/opencv/opencv-python/archive/{version}.zip'
    depends = ['numpy', 'setuptools']
    site_packages_name = 'cv2'
    call_hostpython_via_targetpython = False
    install_in_hostpython = False
    
    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        env['PYTHONPATH'] = ':'.join([
            self.ctx.get_site_packages_dir(),
            env['PYTHONPATH'] if 'PYTHONPATH' in env else ''
        ])
        return env
    
    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        # Ensure the native libraries are properly linked
        # This is a crucial step for OpenCV to work on Android
        libs_dir = self.ctx.get_libs_dir(arch.arch)
        site_packages_dir = self.ctx.get_site_packages_dir()
        cv2_dir = join(site_packages_dir, 'cv2')
        
        # Create the libs directory if it doesn't exist
        if not os.path.exists(libs_dir):
            os.makedirs(libs_dir)
        
        # Copy OpenCV native libraries to the libs directory
        try:
            for lib_file in os.listdir(join('libs', arch.arch)):
                if lib_file.endswith('.so'):
                    src = join('libs', arch.arch, lib_file)
                    dst = join(libs_dir, lib_file)
                    sh.cp('-f', src, dst)
        except (OSError, IOError) as e:
            print(f"Error copying OpenCV libraries: {e}")
        
        # Make sure cv2 can find its native libraries
        # Create a link from site-packages to libs directory if needed
        try:
            if os.path.exists(cv2_dir):
                for lib_file in os.listdir(libs_dir):
                    if lib_file.startswith('libopencv'):
                        src = join(libs_dir, lib_file)
                        dst = join(cv2_dir, lib_file)
                        if not os.path.exists(dst):
                            try:
                                os.symlink(src, dst)
                            except (OSError, IOError):
                                sh.cp('-f', src, dst)
        except (OSError, IOError) as e:
            print(f"Error linking OpenCV libraries: {e}")
            
        return True

recipe = OpenCVRecipe()