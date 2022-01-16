job "weather-sense-monitor" {
  datacenters = ["dc1"]

  group "sensor" {
    # All tasks in a group will run on 
    # the same node
    count = 1
    // network {
    //   port "http" {
    //     static = "5678"
    //   }
    // }

    task "monitor" {
      driver = "exec"

      config {
        command = "python3"

        args = [
          "-listen",
          ":5678",
          "-text",
          "hello world",
        ]
      }
    }
  }
}