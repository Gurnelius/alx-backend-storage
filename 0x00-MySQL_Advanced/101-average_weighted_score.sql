-- Create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE user_id INT;
    DECLARE total_weight INT;
    DECLARE weighted_score_sum FLOAT;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Calculate the total weight of all projects
    SELECT SUM(weight) INTO total_weight FROM projects;

    -- Open the cursor
    OPEN cur;

    -- Loop through all users
    read_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Calculate the weighted score sum for the user
        SELECT SUM(score * weight) INTO weighted_score_sum
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Update the user's average weighted score
        UPDATE users SET average_score = weighted_score_sum / total_weight WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

DELIMITER ;
