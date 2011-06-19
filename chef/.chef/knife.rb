log_level                :info
log_location             STDOUT
node_name                ENV['USER']
client_key               File.expand_path("~/.chef/#{ENV['USER']}.pem")
validation_client_name   'chef-validator'
validation_key           File.join(File.dirname(__FILE__), 'validation.pem')
chef_server_url          'https://api.opscode.com/organizations/hack'
cache_type               'BasicFile'
cache_options( :path => File.expand_path("~/.chef/#{ENV['USER']}/checksums") )
cookbook_path [ File.join(File.dirname(File.dirname(__FILE__)), 'cookbooks'), File.join(File.dirname(File.dirname(__FILE__)), 'public_cookbooks') ]

# Load a user config file if present
if ENV['HOME'] && File.exist?(File.join(ENV['HOME'], '.chef', 'knife.rb'))
  user_config = File.join(ENV['HOME'], '.chef', 'knife.rb')
  instance_eval(IO.read(user_config), user_config, 1)
end

