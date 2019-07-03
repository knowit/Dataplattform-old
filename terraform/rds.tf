resource "aws_db_instance" "dataplattform-aurora" {
    identifier                = "dataplattform-aurora"
    allocated_storage         = 1
    storage_type              = "aurora"
    engine                    = "aurora-mysql"
    engine_version            = "5.7.12"
    instance_class            = "db.t2.medium"
    name                      = "dataplattform"
    username                  = "dataplattform"
    password                  = "xxxxxxxx"
    port                      = 3306
    publicly_accessible       = true
    availability_zone         = "eu-central-1b"
    security_group_names      = []
    vpc_security_group_ids    = ["sg-0583a4e1657cfded3", "sg-0c9b4ed623306c437"]
    db_subnet_group_name      = "default-vpc-02f9ab9c69358eb52"
    parameter_group_name      = "default.aurora-mysql5.7"
    multi_az                  = false
    backup_retention_period   = 1
    backup_window             = "22:42-23:12"
    maintenance_window        = "mon:02:29-mon:02:59"
    final_snapshot_identifier = "dataplattform-aurora-final"
}

