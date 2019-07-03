resource "aws_dynamodb_table" "dataplattform" {
    name = "dataplattform"
    read_capacity = 5
    write_capacity = 5
    hash_key = "type"
    range_key = "timestamp_random"

    attribute {
        name = "timestamp_random"
        type = "B"
    }
    attribute {
        name = "type"
        type = "S"
    }
    tags {
        Project = "Dataplattform"
    }
}
resource "aws_dynamodb_table" "dataplattform_event_codes" {
    name = "dataplattform_event_codes"
    read_capacity = 5
    write_capacity = 5
    hash_key = "event_id"

    attribute {
        name = "event_code"
        type = "S"
    }
    attribute {
        name = "event_id"
        type = "S"
    }
    global_secondary_index {
        name = "event_code-index"
        hash_key = "event_code"
        read_capacity = 5
        write_capacity = 5
        projection_type = "ALL"

    }
}
