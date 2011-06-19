include_recipe "python"

directory "/srv/devopstsdb" do
  owner "www-data"
  group "www-data"
end

python_virtualenv "/srv/devopstsdb/.venv" do
  action :create
  owner "www-data"
  group "www-data"
end

execute "devopstsdb requirements" do
  execute :nothing
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
  notify :execute, 'execute[devopstsdb requirements]'
end


