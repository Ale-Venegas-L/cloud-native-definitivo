resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_launch_configuration" "ecs" {
  name_prefix          = "${var.project_name}-ecs-"
  image_id             = data.aws_ami.amazon_linux_2_ecs.id
  instance_type        = var.instance_type
  iam_instance_profile = aws_iam_instance_profile.ecs.name

  security_groups = [aws_security_group.ecs.id]

  user_data = base64encode(templatefile("${path.module}/userdata_ecs.sh", {
    cluster_name = aws_ecs_cluster.main.name
  }))

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "ecs" {
  name_prefix          = "${var.project_name}-ecs-"
  max_size             = 2
  min_size             = 1
  desired_capacity     = 1
  vpc_zone_identifier  = aws_subnet.private[*].id
  launch_configuration = aws_launch_configuration.ecs.name

  tag {
    key                 = "Name"
    value               = "${var.project_name}-ecs-instance"
    propagate_at_launch = true
  }
}

data "aws_ami" "amazon_linux_2_ecs" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-ecs-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
