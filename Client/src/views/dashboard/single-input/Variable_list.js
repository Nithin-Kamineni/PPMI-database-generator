/* eslint-disable */
import * as React from 'react';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import { ParametersContext } from '../../../context';

const Demo = styled('div')(({ theme }) => ({
    backgroundColor: theme.palette.background.paper
}));

export default function InteractiveList() {
    const useParams = () => React.useContext(ParametersContext);
    let { globalVaribles, DeleteGlobalVaribles } = useParams();
    return (
        <Box>
            <Grid container spacing={2}>
                <Grid item>
                    <Typography variant="h6" component="div">
                        Varibles list
                    </Typography>
                    <Demo>
                        <List dense={true}>
                            {globalVaribles.map((globalVarible, index) => (
                                <ListItem
                                    key={index}
                                    secondaryAction={
                                        <IconButton
                                            edge="end"
                                            aria-label="delete"
                                            onClick={() => {
                                                DeleteGlobalVaribles(globalVarible);
                                            }}
                                        >
                                            <DeleteIcon />
                                        </IconButton>
                                    }
                                >
                                    <ListItemAvatar>
                                        <Avatar>
                                            <FolderIcon />
                                        </Avatar>
                                    </ListItemAvatar>
                                    <ListItemText primary={globalVarible} secondary={'Secondary text'} />
                                </ListItem>
                            ))}
                        </List>
                    </Demo>
                </Grid>
            </Grid>
        </Box>
    );
}
