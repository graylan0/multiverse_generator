from setuptools import setup


setup(
    name='twitch-plays-llm',
    version='0.1.0',
    description='A collaborative twitch-based choose-your-own-adventure game',
    url='https://github.com/Fuehnix/twitch-plays-llm',
    author='Matthew D. Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords='twitch plays llm',
    packages=['twitch_plays_llm'],
    install_requires=[
        'openai',
        'twitchio',
        'pydantic',
        'pydantic_settings',
        'asgiref',
    ],
    extras_require={
        'dev': ['isort', 'blue'],
    },
    entry_points={
        'console_scripts': ['twitch-plays-llm=twitch_plays_llm.__main__:main'],
    },
)
