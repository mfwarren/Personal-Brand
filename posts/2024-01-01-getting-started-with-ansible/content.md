# Getting Started With Ansible

Everyone who does web development will probably find themselves doing devOps tasks at some point. I keep an eye on servers hosting several different projects at different cloud providers and some private servers. Until recently management of those servers wasn't difficult enough to warrant using tools to deal with things.

Ansible is a commandline tool that allows you to manage your servers. Let's say like me you want to introduce it into an environment with servers already in place. Here's how you can get started.

Install the Ansible commandline:

```bash
brew install ansible
```

Create a hosts file (file that lists all the servers you want to manage):

**ansible_hosts:**

```ini
[ec2]
ec2-<something>.compute-1.amazonaws.com  ansible_ssh_private_key_file=/PATH/TO/key.pem  ansible_ssh_user=ec2-user
ec2-<something-else>.compute-1.amazonaws.com  ansible_ssh_private_key_file=/PATH/TO/key.pem  ansible_ssh_user=ec2-user
```

Ping all the servers to see if they respond to ssh:

```bash
ansible ec2 -i ansible_hosts -m ping
```

Ansible comes with a large library of low level 'modules' for doing interesting things on your servers. You can call simple things right from the command line as in the previous example (uses the ping module). If you want to upgrade openssl package on all your (Ubuntu) servers:

```bash
ansible ec2 -i ansible_hosts -m apt -a "name=openssl update_cache=yes" --sudo
```

or upgrade all updates to a CentOS server:

```bash
ansible ec2 -i ansible_hosts -m yum -a "name=* state=latest" --sudo
```

There are over 200 modules built into the core of Ansible to make interacting with lots of different programs easy - git, shell commands, postgres databases, supervisorctl, django, gem packages. Doing a git checkout of your application across a pool of web servers can be done with a single command line.

If that was all you could do with Ansible I'd be happy. But that's really just scratching the surface. Building on these low level modules is what Ansible calls 'roles'. Roles encompass a series of commands to do a bigger task - like install and configure nginx. You can tie multiple roles together into a 'playbook' that can define how to build out your entire infrastructure.

In my next post I'll cover how to go from zero to fully deployed web application with Ansible.
