from setuptools import setup

setup(

    name='resource_pool_secrets_plugin',

    version='0.1',
    author='Ahmad Musa',
    author_email='ahmad@cloudify.co',
    description='the plugin interact with cfy secrets that allocate/unallocate ip for a compute node',
    packages=['plugin'],
    license='LICENSE',
    zip_safe=False,
    install_requires=[
        # Necessary dependency for developing plugins, do not remove!
        "cloudify-common>=4.6"
    ],
    test_requires=[
        "cloudify-common>=4.6"
        "nose"
    ]
)
