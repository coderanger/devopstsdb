include_recipe "python"

directory "/srv/devopstsdb" do
  owner "www-data"
  group "www-data"
end

deploy_revision "/srv/devopstsdb" do
  repository "git://github.com/coderanger/devopstsdb.git"
  user "www-data"
  group "www-data"
  purge_before_symlink []
  create_dirs_before_symlink []
  symlinks({})
  symlink_before_migrate({})
end

python_virtualenv "/srv/devopstsdb/.venv" do
  action :create
  owner "www-data"
  group "www-data"
end

