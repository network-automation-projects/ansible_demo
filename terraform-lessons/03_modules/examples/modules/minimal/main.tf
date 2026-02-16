resource "null_resource" "example" {
  triggers = {
    label = var.label
  }
}
