-- Create the stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_weight INT;
    DECLARE weighted_score_sum FLOAT;

    -- Calculate the total weight of all projects
    SELECT SUM(weight) INTO total_weight FROM projects;

    -- Calculate the weighted score sum for the user
    SELECT SUM(score * weight) INTO weighted_score_sum
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Update the user's average weighted score
    UPDATE users SET average_score = weighted_score_sum / total_weight WHERE id = user_id;
END //

DELIMITER ;
