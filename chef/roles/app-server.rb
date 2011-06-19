name "app-server"
  description "workbench and tools node"
  run_list(
    "role[nginx-server]",
    "role[gunicorn-server]"
  )

