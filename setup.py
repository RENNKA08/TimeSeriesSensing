from setuptools import setup

setup(
    name='tss',
    version='0.1',
    install_requires=[
        'opencv_contrib_python',
        'Pillow',
        'pyserial'
    ],
    description=u'時系列データをより理解しやすい形で記録し、再生するアプリケーションのフレームワーク。',
    author='uMa (Hara-Yuma)',
    url='https://github.com/Hara-Yuma/TimeSeriesSensing',
    packages=['tss']
)
