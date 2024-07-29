/* eslint-disable */

import PropTypes from 'prop-types';
import React, { useContext } from 'react';

// material-ui
import { useTheme } from '@mui/material/styles';
import { Card, CardContent, CardHeader, Divider, Button } from '@mui/material';

import Typography from '@mui/joy/Typography';

import { ParametersContext } from '../../context';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import Sheet from '@mui/joy/Sheet';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import DialogActions from '@mui/joy/DialogActions';
import ModalDialog from '@mui/joy/ModalDialog';
import DeleteForever from '@mui/icons-material/DeleteForever';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import WarningRoundedIcon from '@mui/icons-material/WarningRounded';

// constant
const headerSX = {
    '& .MuiCardHeader-action': { mr: 0 }
};

// ==============================|| CUSTOM MAIN CARD ||============================== //

const MainCard = React.forwardRef(
    (
        {
            border = false,
            boxShadow,
            children,
            content = true,
            contentClass = '',
            contentSX = {},
            darkTitle,
            secondary,
            shadow,
            sx = {},
            title,
            ...others
        },
        ref
    ) => {
        const theme = useTheme();
        const useParams = () => useContext(ParametersContext);
        let { generateGlobalVaribles } = useParams();
        let { setOpen } = useParams();

        return (
            <Card
                ref={ref}
                {...others}
                sx={{
                    border: border ? '1px solid' : 'none',
                    borderColor: theme.palette.mode === 'dark' ? theme.palette.background.default : theme.palette.grey[300] + 98,
                    ':hover': {
                        boxShadow: boxShadow
                            ? shadow ||
                              (theme.palette.mode === 'dark' ? '0 2px 14px 0 rgb(33 150 243 / 10%)' : '0 2px 14px 0 rgb(32 40 45 / 8%)')
                            : 'inherit'
                    },
                    ...sx
                }}
            >
                {/* card header and action */}
                {!darkTitle && title && (
                    <CardHeader
                        sx={headerSX}
                        title={title}
                        action={
                            <>
                                <Button variant="outlined" onClick={() => setOpen(true)} sx={{ marginRight: 2 }}>
                                    <CloudDownloadIcon />
                                </Button>
                                <Button onClick={generateGlobalVaribles} variant="contained" color="primary">
                                    Generate the File
                                </Button>
                            </>
                        }
                    />
                )}
                {darkTitle && title && (
                    <CardHeader
                        sx={headerSX}
                        title={<Typography variant="h3">{title}</Typography>}
                        action={
                            <>
                                <Button variant="outlined" onClick={() => setOpen(true)} sx={{ marginRight: 2 }}>
                                    <CloudDownloadIcon />
                                </Button>
                                <Button variant="contained" color="primary">
                                    Generate the File
                                </Button>
                            </>
                        }
                    />
                )}

                {/* content & header divider */}
                {title && <Divider />}

                {/* card content */}
                {content && (
                    <CardContent sx={contentSX} className={contentClass}>
                        {children}
                    </CardContent>
                )}
                {!content && children}
            </Card>
        );
    }
);

MainCard.propTypes = {
    border: PropTypes.bool,
    boxShadow: PropTypes.bool,
    children: PropTypes.node,
    content: PropTypes.bool,
    contentClass: PropTypes.string,
    contentSX: PropTypes.object,
    darkTitle: PropTypes.bool,
    secondary: PropTypes.oneOfType([PropTypes.node, PropTypes.string, PropTypes.object]),
    shadow: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    sx: PropTypes.object,
    title: PropTypes.oneOfType([PropTypes.node, PropTypes.string, PropTypes.object])
};

export default MainCard;
