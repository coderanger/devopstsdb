name "nginx-server"
  description "workbench and tools node"
  run_list(
    "recipe[nginx]"
  )

