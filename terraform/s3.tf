resource "aws_s3_bucket" "dataplattform-get-docs-cache" {
    bucket = "dataplattform-get-docs-cache"
    tags = {
      Project = "Dataplattform"
      name = "dataplattform-bucket"
    }

   lifecycle_rule {
      abort_incomplete_multipart_upload_days = 0 
      enabled                                = true 
      id                                     = "cleanup_old_data" 
      expiration {
          days                         = 30 
          expired_object_delete_marker = false 
      }
      noncurrent_version_expiration {
          days = 1 
      }
    }
}
