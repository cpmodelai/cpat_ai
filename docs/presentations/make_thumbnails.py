"""Write a preview image of the first slide of every deck in this folder, for the website.

    python make_thumbnails.py     thumbs/<deck name>.png (LibreOffice and pdftoppm)

Run after a deck's _latest copy changes (the deck builders do it; NORMS 5a).
"""
import glob
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs(os.path.join(HERE, 'thumbs'), exist_ok=True)
    for deck in sorted(glob.glob(os.path.join(HERE, '*_latest.pptx'))):
        name = os.path.splitext(os.path.basename(deck))[0]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, deck],
                           check=True, capture_output=True)
            subprocess.run(['pdftoppm', '-png', '-f', '1', '-l', '1', '-scale-to', '640', '-singlefile',
                            os.path.join(tmp, name + '.pdf'), os.path.join(tmp, name)], check=True)
            shutil.move(os.path.join(tmp, name + '.png'), os.path.join(HERE, 'thumbs', name + '.png'))
        print('wrote', f'thumbs/{name}.png')


if __name__ == '__main__':
    main()
