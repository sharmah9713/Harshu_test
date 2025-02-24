resource "aws_iam_role" "eks_fargate_role" {
    name = "eks-fargate-role"

    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [{
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal = {
                Service = "eks-fargate-pods.amazonaws.com"
            }
        }]
    })
}

resource "aws_iam_role_policy_attachment" "eks_fargate_policy" {
    role = aws_iam_role.eks_fargate_role.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
}

resource "aws_eks_fargate_profile" "fargate_profile" {
    cluster_name = aws_eks_cluster.eks.name
    fargate_profile_name = "fargate-profile"
    pod_execution_role_arn = aws_iam_role.eks_fargate_role.arn
    subnet_ids = [ aws_subnet.eks_subnet_1.id ]

    selector {
      namespace = "default"
    }

    depends_on = [ aws_iam_role_policy_attachment.eks_fargate_policy ]
}