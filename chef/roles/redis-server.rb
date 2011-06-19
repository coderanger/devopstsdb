name "redis-server"
  description "workbench and tools node"
  run_list(
    "recipe[redis::source]"
  )

