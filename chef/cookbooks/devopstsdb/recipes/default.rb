include_recipe "python"

directory "/srv/devopstsdb" do
  owner "www-data"
  group "www-data"
end

deploy_revision "/srv/devopstsdb" do
  

python_virtualenv "/srv/devopstsdb/.venv" do
  action :create
  owner "www-data"
  group "www-data"
end

