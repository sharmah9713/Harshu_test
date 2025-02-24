resource "aws_vpc" "eks_vpc" {
    cidr_block = "10.0.0.0/16"
    enable_dns_support = true
    enable_dns_hostnames = true
    tags = { Name = "eks-vpc" }
}

resource "aws_subnet" "eks_subnet_1" {
    vpc_id = aws_vpc.eks_vpc.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = true

    tags = {
        Name = "eks-subnet-1"
    }
}

resource "aws_subnet" "eks_subnet_2" {
    vpc_id = aws_vpc.eks_vpc.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "us-east-1b"
    map_public_ip_on_launch = true

    tags = {
        Name = "eks-subnet-2"
    }
}
