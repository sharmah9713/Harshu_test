resource "aws_iam_role" "eks_cluster_role" {
    name = "eks_cluster_role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "eks.amazonaws.com"
            }
        }]
    })
  }

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
    role = aws_iam_role.eks_cluster_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_eks_cluster" "eks" {
    name = "eks-cluster"
    role_arn = aws_iam_role.eks_cluster_role.arn

    vpc_config {
        subnet_ids = [ aws_subnet.eks_subnet_1.id, aws_subnet.eks_subnet_2.id ]
    }

    tags = {
        Name = "eks-cluster"
    }
    depends_on = [ aws_iam_role_policy_attachment.eks_cluster_policy ]
}