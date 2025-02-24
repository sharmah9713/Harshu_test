resource "aws_eks_fargate_profile" "fargate" {
    cluster_name = aws_eks_cluster.eks.name
    fargate_profile_name = "default"
    pod_execution_role_arn = aws_iam_role.eks_fargate_role.arn
    subnet_ids = [ aws_subnet.eks_subnet_1.id, aws_subnet.eks_subnet_2.id ]

    selector {
      namespace = "default"
    }
}