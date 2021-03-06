include_recipe "python"

package "git-core"

include_recipe "nginx"

directory "/srv/devopstsdb" do
  owner "www-data"
  group "www-data"
end

directory "/srv/devopstsdb/shared" do
  owner "www-data"
  group "www-data"
end

python_virtualenv "/srv/devopstsdb/.venv" do
  action :create
  owner "www-data"
  group "www-data"
end

execute "devopstsdb requirements" do
  action :nothing
  command "/srv/devopstsdb/.venv/bin/pip install -r /srv/devopstsdb/current/app/requirements.txt"
end

deploy_revision "/srv/devopstsdb" do
  repository "git://github.com/coderanger/devopstsdb.git"
  user "www-data"
  group "www-data"
  purge_before_symlink []
  create_dirs_before_symlink []
  symlinks({})
  symlink_before_migrate({})
  notifies :run, 'execute[devopstsdb requirements]', :immediately
end

template "/etc/init/devopstsdb.conf" do
  source "upstart.conf"
  owner "root"
  group "root"
end

service "devopstsdb" do
  provider Chef::Provider::Service::Upstart
  action [:enable, :start]
end

template "/etc/nginx/sites-available/devopstsdb.conf" do
  source "devopstsdb-nginx.conf"
  owner "root"
  group "root"
  notifies :restart, 'service[nginx]', :immediately
end

nginx_site 'default' do
  enable false
end

nginx_site 'devopstsdb.conf'
