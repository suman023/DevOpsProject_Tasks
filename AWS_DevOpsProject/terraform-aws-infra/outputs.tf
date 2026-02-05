output "jenkins_alb_dns" {
  value = aws_lb.jenkins_alb.dns_name
}

