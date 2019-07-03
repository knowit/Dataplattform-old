resource "aws_s3_bucket" "awsknowit" {
    bucket = "awsknowit"
    acl    = "private"
}

resource "aws_s3_bucket" "dataplattform-get-docs-cache" {
    bucket = "dataplattform-get-docs-cache"
    acl    = "private"
}

resource "aws_s3_bucket" "elasticbeanstalk-eu-central-1-275823250475" {
    bucket = "elasticbeanstalk-eu-central-1-275823250475"
    acl    = "private"
    policy = <<POLICY
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "eb-ad78f54a-f239-4c90-adda-49e5f56cb51e",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::275823250475:role/aws-elasticbeanstalk-ec2-role"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::elasticbeanstalk-eu-central-1-275823250475/resources/environments/logs/*"
    },
    {
      "Sid": "eb-af163bf3-d27b-4712-b795-d1e33e331ca4",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::275823250475:role/aws-elasticbeanstalk-ec2-role"
      },
      "Action": [
        "s3:ListBucketVersions",
        "s3:ListBucket",
        "s3:GetObjectVersion",
        "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::elasticbeanstalk-eu-central-1-275823250475",
        "arn:aws:s3:::elasticbeanstalk-eu-central-1-275823250475/resources/environments/*"
      ]
    },
    {
      "Sid": "eb-58950a8c-feb6-11e2-89e0-0800277d041b",
      "Effect": "Deny",
      "Principal": {
        "AWS": "*"
      },
      "Action": "s3:DeleteBucket",
      "Resource": "arn:aws:s3:::elasticbeanstalk-eu-central-1-275823250475"
    }
  ]
}
POLICY
}

resource "aws_s3_bucket" "github-knowit-no" {
    bucket = "github.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "kb-knowit-no" {
    bucket = "kb.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "kionbackupdhcp" {
    bucket = "kionbackupdhcp"
    acl    = "private"
}

resource "aws_s3_bucket" "knowit-docker" {
    bucket = "knowit-docker"
    acl    = "private"
}

resource "aws_s3_bucket" "knowitbilling" {
    bucket = "knowitbilling"
    acl    = "private"
    policy = <<POLICY
{
  "Version": "2008-10-17",
  "Id": "Policy1335892530063",
  "Statement": [
    {
      "Sid": "Stmt1335892150622",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::386209384616:root"
      },
      "Action": [
        "s3:GetBucketAcl",
        "s3:GetBucketPolicy"
      ],
      "Resource": "arn:aws:s3:::knowitbilling"
    },
    {
      "Sid": "Stmt1335892526596",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::386209384616:root"
      },
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::knowitbilling/*"
    }
  ]
}
POLICY
}

resource "aws_s3_bucket" "knowitpublicresources" {
    bucket = "knowitpublicresources"
    acl    = "private"
}

resource "aws_s3_bucket" "labs-knowit-no" {
    bucket = "labs.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "plusstidvalg-knowit-no" {
    bucket = "plusstidvalg.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "registry-aut" {
    bucket = "registry-aut"
    acl    = "private"
}

resource "aws_s3_bucket" "sagemaker-eu-central-1-275823250475" {
    bucket = "sagemaker-eu-central-1-275823250475"
    acl    = "private"
}

resource "aws_s3_bucket" "slack-knowit-no" {
    bucket = "slack.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "teamcity-knowit-no" {
    bucket = "teamcity.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "timer-knowit-no" {
    bucket = "timer.knowit.no"
    acl    = "private"
}

resource "aws_s3_bucket" "vandrepokal-knowit-no" {
    bucket = "vandrepokal.knowit.no"
    acl    = "private"
}

