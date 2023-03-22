from setuptools import setup

package_name = 'security_example'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hypr',
    maintainer_email='hypr@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'MainNode = security_example.security_main_node:main',
            'SecurityServer = security_example.security_server:main',
            'AlarmServer = security_example.alarm_server:main',
            'LoggerServer = security_example.logger_server:main',
        ],
    },
)
