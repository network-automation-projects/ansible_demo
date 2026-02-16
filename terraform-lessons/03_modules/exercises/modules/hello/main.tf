resource "null_resource" "hello" {
  triggers = {
    name = var.name
  }
}
