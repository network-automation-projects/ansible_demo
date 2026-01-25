resource "aws_subnet" "monitoring" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "..."  # Fill this
  availability_zone = "us-east-1a"
  # ...
}

resource "aws_subnet" "servers" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.10.0.0/24"
  availability_zone = "us-east-1a"
  tags = { Name = "servers-subnet" }
}

resource "aws_subnet" "printers" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.10.1.0/26"
  availability_zone = "us-east-1b"
  tags = { Name = "printers-subnet" }
}