module "web" {
  source = "../../modules/docker-web"

  image_name     = "nginx:alpine"
  container_name = "ziad-dev-web"
  external_port  = 8080
}
