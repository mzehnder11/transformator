import os
import subprocess
import shutil
import customtkinter

def build():
    # Paths
    project_dir = os.getcwd()
    ctk_path = os.path.dirname(customtkinter.__file__)
    
    # Command arguments
    args = [
        'python', '-m', 'PyInstaller',
        '--noconfirm',
        '--onedir',
        '--windowed',
        f'--add-data={ctk_path}{os.pathsep}customtkinter',
        '--collect-all=imageio',
        '--collect-all=moviepy',
        '--hidden-import=pillow_avif',
        '--hidden-import=fpdf',
        '--icon=icon.ico',
        '--name=TransformatorPro',
        'app.py'
    ]
    
    print(f"Running command: {' '.join(args)}")
    subprocess.run(args, check=True)
    
    print("\nBuild complete. Check the 'dist' folder.")

if __name__ == "__main__":
    build()
